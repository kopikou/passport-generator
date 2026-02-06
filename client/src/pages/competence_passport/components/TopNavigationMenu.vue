<script setup lang="ts">
import PlanListView from '../PlanListView.vue'
import { watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCompetencePassportStore } from 'src/stores/competencePassportStore'
import { storeToRefs } from 'pinia'

const route = useRoute()
const router = useRouter()
const store = useCompetencePassportStore()
const { currentPlanId,
  isMatrixValid,
 } = storeToRefs(store)

// Определяем активную вкладку по текущему пути
const currentTab = computed(() => {
  if (route.path.includes('/matrix')) return 'matrix'
  if (route.path.includes('/schema')) return 'schema'
  if (route.path.includes('/passport')) return 'passport'
  return 'reference'
})

// Защита маршрутов: перенаправление, если матрица не валидна
// watch(
//   () => route.path,
//   async (newPath) => {
//     const requiresValidMatrix = route.meta?.requiresValidMatrix as boolean
//     if (requiresValidMatrix && !isMatrixValid) {
//       await router.push({ name: 'competenceMatrix' })
//     }
//   },
//   { immediate: true }
// )

// Генерация путей для вкладок
const getTabPath = (tabName: string): string => {
  if (!currentPlanId) return '#'
  const id = currentPlanId
  switch (tabName) {
    case 'reference': return `/competence-passport/${id}/competences`
    case 'matrix': return `/competence-passport/${id}/matrix`
    case 'schema': return `/competence-passport/${id}/schema`
    case 'passport': return `/competence-passport/${id}/passport`
    default: return '#'
  }
}
</script>

<template>
  <PlanListView>
    <template #contents>
      <div class="top-navigation-layout q-pb-xl">
        <q-tabs
          class="text-black"
          align="left"
          indicator-color="primary"
        >
          <q-route-tab
            name="reference"
            label="Справочники"
            :to="getTabPath('reference')"
            exact
          />
          <q-route-tab
            name="matrix"
            label="Матрица"
            :to="getTabPath('matrix')"
            exact
          />
          <q-route-tab
            name="schema"
            label="Схема"
            :to="getTabPath('schema')"
            :disable="!isMatrixValid"
            exact
          />
          <q-route-tab
            name="passport"
            label="Паспорт"
            :to="getTabPath('passport')"
            :disable="!isMatrixValid"
            exact
          />
        </q-tabs>

        <div class="content-area q-pb-xl">
          <slot name="content"/>
        </div>
      </div>

    </template>
  </PlanListView>
</template>

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

.q-tabs {
  background: $grey-4;
  border-bottom: 2px solid silver;
  box-shadow: 0 0 8px silver;
}
</style>