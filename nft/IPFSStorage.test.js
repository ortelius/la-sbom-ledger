const MockIPFSStorage = require('./IPFSStorage.mock')

describe('IPFStorage', () => {
	test('should produce same cid for minified sbom data with same content', async () => {
		const mockIPFSStorage = new MockIPFSStorage()

		const cid1 = await mockIPFSStorage.upload(
			'../test/resource/sample_sbom_1.json'
		)

		const cid2 = await mockIPFSStorage.upload(
			'../test/resource/sample_sbom_2.json'
		)

		expect(cid1).toEqual(cid2)
	})
})
