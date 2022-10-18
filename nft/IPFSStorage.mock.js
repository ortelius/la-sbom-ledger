const fs = require('fs')
const crypto = require('crypto')

class MockIPFSStorage {
	async upload(filePath) {
		const data = JSON.parse((await fs.promises.readFile(filePath)).toString())

		const minified = Buffer.from(JSON.stringify(data, null, 0), 'utf-8')

		const cid = await this.#createHash(minified)
		const status = ''
		const metadata = ''

		return { cid, status, metadata }
	}

	async #createHash(value) {
		return crypto.createHash('sha256').update(value).digest('hex')
	}
}

module.exports = MockIPFSStorage
