import {defineStore} from "pinia";
import {onBeforeMount, ref} from "vue";
import {api} from "boot/axios";
import {useRouter} from "vue-router";

const useMainStore = defineStore("MainStore", () => {
  const username = ref("");
  const userId = ref(-1);
  const firstName = ref("");
  const lastName = ref("");
  const mira_id = ref(-1)
  const isAuthenticated = ref(false);
  const isSuperuser = ref(false);
  const isStaff = ref(false);
  const BITRIX_CLIENT_ID = ref("");
  const FORCE_SCRIPT_NAME = ref("");
  const VISIT_TOKEN_TIMEOUT = ref(30);
  const csrf = ref('');
  const permissions = ref<Permissions[]>([]);

  const rop = ref(false)
  const can_upload = ref(false)

  const router = useRouter();

  async function checkLogin() {
    let r = await api.get('/api/user/checkLogin/')
    let data = r.data;
    // console.log(data)
    isAuthenticated.value = data.authenticated;
    isSuperuser.value = data.is_superuser;
    isStaff.value = data.is_staff;
    username.value = data.username;
    userId.value = data.user_id;
    firstName.value = data.first_name;
    lastName.value = data.last_name;
    mira_id.value = data.mira_id
    permissions.value = data.permissions;
    BITRIX_CLIENT_ID.value = r.data.BITRIX_CLIENT_ID
    FORCE_SCRIPT_NAME.value = r.data.FORCE_SCRIPT_NAME
    VISIT_TOKEN_TIMEOUT.value = r.data.VISIT_TOKEN_TIMEOUT
    csrf.value = r.data.csrf
    can_upload.value = r.data.can_upload
    rop.value = r.data.rop


    api.defaults.headers.common['X-CSRFToken'] = r.data.csrf

    let baseTag = document.querySelector("base")
    if (baseTag)
      baseTag.href = FORCE_SCRIPT_NAME.value;

    if (!isAuthenticated.value) {
      // document.location.href = `https://int.istu.edu/oauth/authorize/?client_id=${BITRIX_CLIENT_ID.value}&state=next:${encodeURIComponent(window.location.href.toString())}`;
      document.location.href = `${FORCE_SCRIPT_NAME.value}/api/esia/login/`
    }
  }


  return {
    username,
    isAuthenticated,
    isSuperuser,
    isStaff,
    firstName,
    lastName,
    mira_id,
    userId,
    BITRIX_CLIENT_ID,
    FORCE_SCRIPT_NAME,
    VISIT_TOKEN_TIMEOUT,
    csrf,
    can_upload,
    rop,
    permissions,
    checkLogin,
  }
})


export default useMainStore;
