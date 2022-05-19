import CryptoJS from 'crypto-js';


/**
 * AES加密
 * @param content 待加密内容
 * @param key 加密密钥
 * @param iv 加密向量
 * @returns {*} 加密后的内容
 */
const encrypt = (content,key,iv) => {
    return CryptoJS.AES.encrypt(CryptoJS.enc.Utf8.parse(content), CryptoJS.enc.Utf8.parse(key), {
        mode: CryptoJS.mode.CBC,
        iv: CryptoJS.enc.Utf8.parse(iv),
        padding: CryptoJS.pad.Pkcs7
    }).toString();
};

/**
 * AES解密
 * @param ciphertext 已加密内容
 * @param key 解密密钥
 * @param iv 解密向量
 * @returns {*} 解密后内容
 */
const decrypt = (ciphertext,key,iv) => {
    return CryptoJS.AES.decrypt(ciphertext, CryptoJS.enc.Utf8.parse(key), {
        mode: CryptoJS.mode.CBC,
        iv: CryptoJS.enc.Utf8.parse(iv),
        padding: CryptoJS.pad.Pkcs7
    }).toString(CryptoJS.enc.Utf8);
};


module.exports = {
    encrypt, decrypt
};
