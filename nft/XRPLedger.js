const xrpl = require('xrpl')

const XRP_DEVNET_WALLET = {
	classicAddress: 'rnPjPkpLX22qoEow3Swd7DHhm4cB3bvd7g',
	secret: 'snRyfCfvZR1hxmnqMf37ZcG9vtLfX',
	sequenceNumber: '945040'
}

const XRP_DEVNET_URL = 'wss://xls20-sandbox.rippletest.net:51233'

class XRPLedger {
	constructor(network = XRP_DEVNET_URL, wallet = XRP_DEVNET_WALLET) {
		this.network = network
		this.wallet = xrpl.Wallet.fromSeed(wallet.secret)
	}

	async mintToken(ipfsUrl) {
		const client = await this.connect()

		console.log('start minting...')

		const transaction = {
			TransactionType: 'NFTokenMint',
			Account: this.wallet.classicAddress,
			URI: xrpl.convertStringToHex(ipfsUrl),
			Flags: parseInt(0),
			TokenTaxon: 0 //Required, but if you have no use for it, set to zero.
		}

		const transactionResult = await client.submitAndWait(transaction, {
			wallet: this.wallet
		})

		console.log('minting done...')

		client.disconnect()

		return transactionResult
	}

	async connect() {
		const client = new xrpl.Client(this.network)
		await client.connect()

		console.log('xrp client connected to ' + this.network)

		return client
	}

	async getTokens() {
		const client = await this.connect()

		const tokens = await client.request({
			method: 'account_nfts',
			account: this.wallet.classicAddress
		})

		client.disconnect()

		return tokens
	}

	async getWallet() {
		const wallet = xrpl.Wallet.fromSeed(wallet.secret)

		return wallet
	}
}

module.exports = new XRPLedger()
