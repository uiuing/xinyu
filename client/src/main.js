import Vue from 'vue';
import App from './App';
import uView from "uview-ui";
import management_status from '@/config/management_status';
import axios from '@/lib/axios';
import base64 from "@/utils/characterManipulation/Base64";

Vue.config.productionTip = false;

App.mpType = 'app';

const app = new Vue({
    ...App
});

Vue.prototype.$utils = {base64: base64};
Vue.prototype.$memory = management_status;
Vue.prototype.$http = axios;


Vue.use(uView);
app.$mount();