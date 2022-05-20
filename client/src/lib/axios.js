import axios from "axios";
import async from "async";

axios.defaults.baseURL = "";

const sign = {
    async sendCode(phoneNumber) {
        return await axios.post("/sign/sendCode", {
            phoneNumber: phoneNumber
        });
    },
    async verifyCode(phoneNumber, code) {
        return await axios.post("/sign/verifyCode", {
            phoneNumber: phoneNumber,
            code: code
        });
    },
    async modifyNickname(user_id, nick_name) {
        return await axios.post("/sign/modifyNickname", {
            user_id: user_id,
            nick_name: nick_name
        });
    },
    async getNickName(user_id) {
        return await axios.post("/sign/getNickName", {
            user_id: user_id
        });
    },
    async getAuthentication(nick_name) {
        return await axios.post("/sign/getAuthentication", {
            nick_name: nick_name
        });
    }
};

const content = {
    async add(user_id, content, open_permissions) {
        return await axios.post("/content/add", {
            user_id: user_id,
            content: content,
            open_permissions: open_permissions
        });
    },
    async getHistory(user_id) {
        return await axios.post("/content/get_history", {
            user_id: user_id
        });
    },
    async delete(content_id) {
        return await axios.post("/content/delete", {
            content_id: content_id
        });
    },
    async getRecommendContent(user_id) {
        return await axios.post("/content/get_recommend_content", {
            user_id: user_id
        });
    }
};

const message = {
    async add(production_id, consumption_id, content_id, content) {
        return await axios.post("/message/dialogue/add", {
            production_id: production_id,
            consumption_id: consumption_id,
            content_id: content_id,
            content: content
        });
    },
    async dialogue(dialogue_id) {
        return await axios.post("/message/dialogue", {
            dialogue_id: dialogue_id
        });
    },
    async getDialogueContent(content_id) {
        return await axios.post("/message/get_dialogue/content", {
            content_id: content_id
        });
    },
    async getDialogueUser(user_id) {
        return await axios.post("/message/get_dialogue/user", {
            user_id: user_id
        });
    },
    async getUserUnreadCount(user_id) {
        return await axios.post("/message/dialogue/user/unread_count", {
            user_id: user_id
        });
    },
    async userUnreadAdd(user_id,dialogue_id,number_unread) {
        return await axios.post("/message/dialogue/user/unread_add", {
            user_id: user_id,
            dialogue_id: dialogue_id,
            number_unread: number_unread
        });
    },
    async userRead(user_id,dialogue_id) {
        return await axios.post("/message/dialogue/user/read", {
            user_id: user_id,
            dialogue_id: dialogue_id
        });
    },
    async userUnreadList(user_id) {
        return await axios.post("/message/dialogue/user/unread_list", {
            user_id: user_id
        });
    }
};

module.exports = {
    sign,
    content,
    message
};