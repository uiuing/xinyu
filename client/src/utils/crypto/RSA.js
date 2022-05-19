import JSEncrypt from 'jsencrypt'

/**
 * Encrypts data with RSA public key
 * @param data data to encrypt
 * @param publicKey RSA public key
 * @returns {string | false} encrypted data or false if error
 */
const encrypt = (data,publicKey) => {
  const encrypt = new JSEncrypt()
  encrypt.setPublicKey(publicKey)
    console.log(encrypt.encrypt(data))
  return encrypt.encrypt(data)
}

/**
 * Decrypts data with RSA private key
 * @param data data to decrypt
 * @param privateKey RSA private key
 * @returns {string | false} decrypted data or false if error
 */
const decrypt = (data,privateKey) => {
  const decrypt = new JSEncrypt()
  decrypt.setPrivateKey(privateKey)
  return decrypt.decrypt(data)
}

module.exports = {
  encrypt,
  decrypt
}