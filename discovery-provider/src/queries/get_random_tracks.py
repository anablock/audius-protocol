import logging  # pylint: disable=C0302
import datetime
from dateutil.parser import parse

from src.utils.db_session import get_db_read_replica
from src.queries.get_unpopulated_tracks import get_unpopulated_tracks
from src.queries.query_helpers import populate_track_metadata, \
    get_users_ids, get_users_by_id
from src.tasks.generate_trending import generate_trending
from src.utils.redis_cache import use_redis_cache

logger = logging.getLogger(__name__)

def make_random_cache_key(time_range, genre, limit, exclusion_list):
    """Makes a cache key resembling `generated-trending:week:electronic`"""
    return f"generated-random:{time_range}:{(genre.lower() if genre else '')}:{limit}:{''.join(exclusion_list)}"

def generate_unpopulated_random(session, genre, limit, exclusion_list, time_range):
    trending_tracks = generate_trending(
        session, time_range, genre, limit, 0
    )
    filtered_trending_tracks = list(filter(lambda track: track['track_id'] in exclusion_list))

    track_scores = [z(time_range, track) for track in trending_tracks['listen_counts']]
    sorted_track_scores = sorted(track_scores, key=lambda k: k['score'], reverse=True)

    track_ids = [track['track_id'] for track in sorted_track_scores]

    tracks = get_unpopulated_tracks(session, track_ids)
    return (tracks, track_ids)

def make_generate_unpopulated_random(session, genre, limit, exclusion_list, time_range):
    """Wraps a call to `generate_unpopulated_trending` for use in `use_redis_cache`, which
       expects to be passed a function with no arguments."""
    def wrapped():
        return generate_unpopulated_random_(session, genre, limit, exclusion_list, time_range)
    return wrapped


N = 1
a = max
M = pow
F = 50
O = 1
R = 0.25
i = 0.01
q = 20.0
T = {'day': 1, 'week':7, 'month':30, 'year':365, 'allTime': 100000}
def z(time, track):
    # pylint: disable=W,C,R
    E=track['listens']
    e=track['windowed_repost_count']
    t=track['repost_count']
    x=track['windowed_save_count']
    A=track['save_count']
    o=track['created_at']
    l=track['track_owner_follower_count']
    j=track['karma']
    if l<3:
        return{'score':0,**track}
    H=(N*E+F*e+O*x+R*t+i*A)*j
    L=T[time]
    K=datetime.datetime.now()
    w=parse(o)
    k=(K-w).days
    Q=1
    if k>L:
        Q=a((1.0/q),(M(q,(1-k/L))))
    return{'score':H*Q,**track}

def get_random_tracks(args):
    """Gets trending by getting the currently cached tracks and then populating them."""
    db = get_db_read_replica()
    with db.scoped_session() as session:
        genre, limit, exclusion_list = args.get("genre"), args.get("limit"), args.get("exclusion_list")
        query_time = "week"
        key = make_random_cache_key(query_time, genre, limig, exclusion_list)

        # Will try to hit cached trending from task, falling back
        # to generating it here if necessary and storing it with no TTL
        (tracks, track_ids) = use_redis_cache(key, None, make_generate_unpopulated_random(
            session, genre, limit, exclusion_list, query_time
        ))

        # Re-sort the populated tracks b/c it loses sort order in sql query
        sorted_tracks = [tracks_map[track_id] for track_id in track_ids]
        return sorted_tracks
