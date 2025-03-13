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
  const VISIT_TOKEN_TIMEOUT = ref(30);
  const csrf = ref('');
  const permissions = ref<Permissions[]>([]);

  const router = useRouter();

  async function checkLogin() {
    let r = await api.get('api/user/checkLogin/')
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
    VISIT_TOKEN_TIMEOUT.value = r.data.VISIT_TOKEN_TIMEOUT
    csrf.value = r.data.csrf
    api.defaults.headers.common['X-CSRFToken'] = r.data.csrf

    if (!isAuthenticated.value) {
      document.location.href = `https://int.istu.edu/oauth/authorize/?client_id=${BITRIX_CLIENT_ID.value}`;
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
    VISIT_TOKEN_TIMEOUT,
    csrf,
    permissions,
    checkLogin,
  }
})


export default useMainStore;
