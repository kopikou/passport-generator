<script setup lang="ts">
import {computed, onBeforeMount, ref, watch} from "vue";
import {api} from "boot/axios";
import {LocalStorage, SessionStorage, useQuasar} from "quasar";
import {storeToRefs} from "pinia";
import _ from "lodash";
import useMainStore from "stores/mainStore";

const tab = ref('my')
</script>

<template>
  <q-tabs
    v-model="tab"
    class="text-teal"
  >
    <q-tab name="my" label="Мой план" />
    <q-tab name="all" label="Все планы" />
  </q-tabs>
</template>

<style scoped>

</style>
