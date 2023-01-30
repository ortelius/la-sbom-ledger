const fs = require('fs').promises

const MockIPFSStorage = require('./IPFSStorage.mock')

const FIRST_SBOM_FILE_PATH = '../test/resource/sample_sbom_1.json'
const SECOND_SBOM_FILE_PATH = '../test/resource/sample_sbom_2.json'

describe('IPFStorage', () => {
	const mockIPFSStorage = new MockIPFSStorage()

	test('should produce same cid for minified sbom data with same content', async () => {
		const cid1 = await mockIPFSStorage.upload(FIRST_SBOM_FILE_PATH)

		const cid2 = await mockIPFSStorage.upload(SECOND_SBOM_FILE_PATH)

		expect(cid1).toEqual(cid2)
	})

	test('should transpose nft into sbom file', async () => {
		const { cid } = await mockIPFSStorage.upload(FIRST_SBOM_FILE_PATH)

		let uploadedSBOM = await fs.readFile(FIRST_SBOM_FILE_PATH)

		let minifiedUploadedSBOM = Buffer.from(
			JSON.stringify(uploadedSBOM, null, 0),
			'utf-8'
		)

		let retrievedNFTData = await fs.readFile(`${cid}.json`)

		expect(minifiedUploadedSBOM.toString() === retrievedNFTData.toString())

		fs.unlink(`${cid}.json`)
	})
})
