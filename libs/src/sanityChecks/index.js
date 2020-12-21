const isCreator = require('./isCreator')
const sanitizeNodes = require('./sanitizeNodes')
const addSecondaries = require('./addSecondaries')
const syncNodes = require('./syncNodes')
const rolloverNodes = require('./rolloverNodes')
const recoveryEmail = require('./needsRecoveryEmail')
const assignReplicaSet = require('./assignReplicaSet')

// Checks to run at startup to ensure a user is in a good state.
class SanityChecks {
  constructor (libsInstance) {
    this.libs = libsInstance
  }

  /**
   * Runs sanity checks
   * @param {Set<string>} creatorNodeWhitelist
   */
  async run (creatorNodeWhitelist = null) {
    await isCreator(this.libs)
    await sanitizeNodes(this.libs)
    await addSecondaries(this.libs)
    await syncNodes(this.libs)
    await rolloverNodes(this.libs, creatorNodeWhitelist)
    await recoveryEmail(this.libs)
    await assignReplicaSet(this.libs, creatorNodeWhitelist)
  }
}

module.exports = SanityChecks
