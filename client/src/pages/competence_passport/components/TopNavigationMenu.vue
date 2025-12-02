<template>
  <div class="top-navigation-layout">
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

    <!-- Используем слот content для размещения контента -->
    <div class="content-area">
      <slot name="content">
        <!-- Fallback если слот не передан -->
        <slot></slot>
      </slot>
    </div>
  </div>
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

defineExpose({ currentTab })
</script>

<style scoped lang="scss">
.top-navigation-layout {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.content-area {
  flex: 1;
  overflow-y: auto;
}
</style>