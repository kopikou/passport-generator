<script setup lang="ts">
import useMainStore from "stores/mainStore";
import {storeToRefs} from "pinia";

const mainStore = useMainStore();
const {
  isAuthenticated,
  isStaff,
  lastName,
  firstName,
} = storeToRefs(mainStore)

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
            Система управления рабочими программами
          </q-btn>

        </q-toolbar-title>

        <q-tabs inline-label dense shrink stretch v-if="isAuthenticated">
          <q-route-tab icon="mdi-format-list-checks" label="Список файлов" to="/" />
          <q-route-tab icon="mdi-upload" label="Загрузка файлов" to="/upload" />
          <q-btn-dropdown auto-close stretch flat :label="`${lastName} ${firstName}`">
            <q-list>
              <q-item clickable href="/admin/" v-if="isStaff">
                <q-item-section>Админка</q-item-section>
              </q-item>
              <q-item clickable href="/api/accounts/logout/">
                <q-item-section>Выйти</q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>
        </q-tabs>
      </q-toolbar>
    </q-header>

    <q-page-container class="container">
      <q-page style="overflow: hidden">
        <router-view/>
      </q-page>
    </q-page-container>
  </q-layout>

</template>

<style scoped>

</style>
