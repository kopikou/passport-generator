<script setup lang="ts">
import useMainStore from "stores/mainStore";
import {storeToRefs} from "pinia";
import {api} from "boot/axios";
import {useQuasar} from "quasar";
import {Permissions} from "src/types";
import {onBeforeMount, ref} from "vue";
import _ from "lodash";
import useUploadFileViewStore from "stores/uploadFileViewStore";

const mainStore = useMainStore();
const {
  isAuthenticated,
  isStaff,
  lastName,
  firstName,
  permissions,
  can_upload,
  FORCE_SCRIPT_NAME,
} = storeToRefs(mainStore)


const $q = useQuasar()

api.interceptors.response.use((response) => response, (error) => {
  $q.loading.hide()
  if (error.code != "ERR_CANCELED") {
    $q.notify({
      color: 'negative',
      message: error.response?.data?.detail || 'Ошибка получения данных, перезагрузите страницу',
      icon: 'mdi-alert-box',
      position: 'top',
    })
    throw error
  }
})


onBeforeMount(async () => {
  if (!isAuthenticated.value) {
    await mainStore.checkLogin()
  }
})

</script>

<template>

  <q-layout view="hHh lpR fFf">
    <q-header elevated class="bg-white text-black">
      <q-toolbar>
        <q-toolbar-title to="/">
          <q-btn round color="white" flat to="/">
            <q-avatar>
              <img src="~assets/istu_logo.png">
            </q-avatar>
          </q-btn>
          <q-btn to="/" flat v-if="!$q.screen.xs">
            Управление рабочими программами
          </q-btn>
        </q-toolbar-title>
        <q-tabs inline-label dense shrink stretch v-if="isAuthenticated">
          <q-route-tab icon="mdi-upload-box" label="Загрузка файлов программ" to="/upload"
                       v-show="can_upload"
          />
          <q-route-tab icon="mdi-generator-portable" label="РПД" to="/generator"
                       v-permissions-required="Permissions.can_use_generator"
          />
<!--          <q-route-tab icon="mdi-generator-mobile" label="РПП" to="/practice_generator"-->
<!--                       v-permissions-required="Permissions.can_use_generator"-->
<!--          />-->
          <q-route-tab icon="mdi-account-school" label="План научной деятельности аспирантуры"
                       to="/scientific-plan"
                       v-permissions-required="Permissions.can_use_generator"
          />
          <q-route-tab icon="mdi-format-list-checks" label="PLX файлы" to="/plx"
                       v-permissions-required="Permissions.can_upload_plx_files"
          />
          <q-btn-dropdown auto-close stretch flat :label="`${lastName} ${firstName}`">
            <q-list>
              <q-item clickable :href="`${FORCE_SCRIPT_NAME}/admin/`" v-if="isStaff">
                <q-item-section>Админка</q-item-section>
              </q-item>
              <q-item clickable href="https://int.istu.edu/">
                <q-item-section>Назад в кампус</q-item-section>
              </q-item>
              <q-item clickable :href="`${FORCE_SCRIPT_NAME}/api/accounts/logout/`">
                <q-item-section>Выйти</q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>
        </q-tabs>
      </q-toolbar>
    </q-header>

    <q-page-container class="container">
      <q-page style="overflow: hidden">
        <router-view v-slot="{ Component }">
            <component :is="Component" />
        </router-view>
      </q-page>
    </q-page-container>
  </q-layout>

</template>

<style scoped>

</style>
