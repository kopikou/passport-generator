<template>
  <q-tabs
    v-model="currentTab"
    class="bg-primary text-white shadow-2"
    align="left"
    indicator-color="white"
  >
    <q-route-tab
      name="reference"
      label="Справочники"
      to="/competence/reference"
      exact
    />
    <q-route-tab
      name="matrix"
      label="Матрица"
      to="/competence/matrix"
      exact
    />
    <q-route-tab
      name="schema"
      label="Схема"
      to="/competence/schema"
      exact
    />
    <q-route-tab
      name="passport"
      label="Паспорт"
      to="/competence/passport"
      exact
    />
  </q-tabs>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const currentTab = ref('reference')

watch(
  () => route.path,
  (newPath) => {
    if (newPath.includes('/matrix')) currentTab.value = 'matrix'
    else if (newPath.includes('/schema')) currentTab.value = 'schema'
    else if (newPath.includes('/passport')) currentTab.value = 'passport'
    else currentTab.value = 'reference'
  },
  { immediate: true }
)
</script>