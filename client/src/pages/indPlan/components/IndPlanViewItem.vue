<script setup lang="ts">
import {computed, onBeforeMount, ref, watch} from "vue";
import {api} from "boot/axios";

const tab = ref('first')
</script>

<template>
  <q-tabs
    v-model="tab"
    class="text-teal"
  >
    <q-tab name="first" label="1 - Учебная нагрузка" />
    <q-tab name="second" label="2 - Подготовка к учебным занятиям" />
    <q-tab name="third" label="3 - Учебно-методическая работа" />
    <q-tab name="fourth" label="4 - Иные виды работ" />
    <q-tab name="fifth" label="5 - Работа с обучающимися и абитуриентами" />
  </q-tabs>
</template>

<style scoped>

</style>
