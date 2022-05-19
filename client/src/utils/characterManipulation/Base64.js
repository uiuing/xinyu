//字符串转base64
function encode(str) {
    // 对字符串进行编码，并将编码的字符串转化base64
    return btoa(encodeURI(str));
}

// base64转字符串
function decode(base64) {
    // 对base64转编码，并将编码转字符串
    return decodeURI(atob(base64));
}

export default {
    encode,
    decode
}