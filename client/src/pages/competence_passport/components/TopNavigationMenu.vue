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
        :to="schemaRoute"
        :disable="!isMatrixValid"
        exact
      />
      <q-route-tab
        name="passport"
        label="Паспорт"
        :to="passportRoute"
        :disable="!isMatrixValid"
        exact
      />
    </q-tabs>

    <div class="content-area">
      <slot name="content">
        <slot></slot>
      </slot>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCompetencePassportStore } from 'stores/competencePassportStore'

const route = useRoute()
const router = useRouter()
const store = useCompetencePassportStore()
const currentTab = ref('reference')

const schemaRoute = computed(() => {
  return isMatrixValid.value ? '/competence/schema' : ''
})

const passportRoute = computed(() => {
  return isMatrixValid.value ? '/competence/passport' : ''
})

const isMatrixValid = computed(() => {
  if (!store.currentPlanId) return false
  
  if (store.matrixValidation.isValid) return true

  return localStorage.getItem(`matrix_valid_${store.currentPlanId}`) === 'true'
})

watch(
  () => store.matrixValidation.isValid,
  (isValid) => {
    if (isValid && store.currentPlanId) {
      localStorage.setItem(`matrix_valid_${store.currentPlanId}`, 'true')
    }
  }
)

// Защита от перехода на заблокированные страницы
watch(
  () => route.path,
  (newPath) => {
    if (newPath.includes('/matrix')) currentTab.value = 'matrix'
    else if (newPath.includes('/schema')) currentTab.value = 'schema'
    else if (newPath.includes('/passport')) currentTab.value = 'passport'
    else currentTab.value = 'reference'

    if ((newPath.includes('/schema') || newPath.includes('/passport')) && !isMatrixValid.value) {
      router.push({ name: 'competenceMatrix' })
    }
  },
  { immediate: true }
)

defineExpose({ currentTab, isMatrixValid })
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
  display: flex;
  flex-direction: column;
}

.q-tab--disabled {
  opacity: 0.5;
  cursor: not-allowed;

}
</style>