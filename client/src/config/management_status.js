/**
 * @file memory变量配置 管理当前状态
 */


/**
 * @description 屏幕可滚动的高度
 * @type {number}
 */
const scrollerHeight = document.body.scrollHeight;

/**
 * @description 用户登录状态管理
 * @property {String} userId 用户id
 * @type {{
 *          isLogin,userId,userName
 *          init: userStatus.init, set: userStatus.set, clear: userStatus.clear
 * }}
 */
const userStatus = {

    /**
     * @description 初始化用户登录状态
     */
    init: () => {
        let user_status = localStorage.getItem("caching:user_status");
        if (user_status) {
            try {
                user_status = JSON.parse(decodeURI(atob(user_status)));
                userStatus.isLogin = true;
                userStatus.userId = user_status.userId;
                userStatus.nickName = decodeURI(atob(user_status.nickName));
            } catch (e) {
                userStatus.clear();
            }
        } else {
            userStatus.isLogin = false;
        }
    },

    /**
     * @description 用户移除登录状态
     */
    clear: () => {
        localStorage.removeItem("caching:user_status");
        userStatus.isLogin = false;
    },

    /**
     * @description 设置用户ID
     * @param {String} userId 用户id
     */
    set: (userId,nickName) => {
        localStorage.setItem("caching:user_status", btoa(encodeURI(JSON.stringify({
            userId: userId,
            nickName:nickName
        }))));
        userStatus.isLogin = true;
        userStatus.userId = userId;
        userStatus.nickName = decodeURI(atob(nickName));
    },
};

/**
 * @description 用户草稿内容管理
 */
const draftContent = {
    /**
     * @description 初始化用户草稿内容
     */
    init: () => {
        let content = localStorage.getItem("caching:draftContent");
        if (content) {
            try {
                draftContent.content = decodeURI(atob(content));
            } catch (e) {
                draftContent.clear();
            }
        } else {
            draftContent.content = '';
        }
    },
    /**
     * @description 用户移除草稿内容
     */
    clear: () => {
        localStorage.removeItem("caching:draftContent");
        draftContent.content = '';
    },

    /**
     * @description 设置用户创作草稿内容
     * @param {String} content 草稿内容
     */
    set: (content) => {
        localStorage.setItem("caching:draftContent", btoa(encodeURI(content)));
        draftContent.content = content;
    }
};

module.exports = {
    scrollerHeight: scrollerHeight, userStatus: userStatus, draftContent: draftContent
};