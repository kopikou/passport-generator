<script setup lang="ts">
import { computed, onBeforeMount } from 'vue'
import { useRoute } from 'vue-router'
import TopNavigationMenu from './TopNavigationMenu.vue'
import ReferenceLeftMenu from './ReferenceLeftMenu.vue'
import PassportLeftMenu from './PassportLeftMenu.vue'
import { useCompetencePassportStore } from 'src/stores/competencePassportStore'
import { storeToRefs } from 'pinia'

const store = useCompetencePassportStore()
const {
  currentPlanId
} = storeToRefs(store)

const route = useRoute()

// Определяем, какое меню показывать
const currentSidebar = computed(() => {
  const name = route.name?.toString()

  if (name?.startsWith('competencesReference') || name?.startsWith('disciplinesReference')) {
    return ReferenceLeftMenu
  }

  if (name?.startsWith('competencePassport')) {
    return PassportLeftMenu
  }

  return null
})

const showSidebar = computed(() => currentSidebar.value !== null)

// Загрузка данных
async function loadData() {
  //await store.fetchCompetencePassport(currentPlanId.value)
  await store.fetchPlanAdmissionData(currentPlanId.value)
  //await store.fetchReferences(currentPlanId.value)
}

onBeforeMount(() => {
  if (currentPlanId.value) loadData()
})
</script>

<template>
  <TopNavigationMenu>
    <template #content>
      <div class="layout-content">
        <!-- Боковое меню -->
        <aside v-if="showSidebar" class="sidebar">
          <component :is="currentSidebar" />
        </aside>

        <!-- Основной контент -->
        <main class="main-content" :class="{ 'full-width': !showSidebar }">
          <router-view />
        </main>
      </div>
    </template>
  </TopNavigationMenu>
</template>

<style scoped lang="scss">
.layout-content {
  height: 100%;
  display: flex;
  overflow: hidden;
}

.sidebar {
  width: 20%;
  border-right: 2px solid silver;
  box-shadow: 0 0 8px silver;
  overflow-y: auto;
  flex-shrink: 0;
}

.main-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;

  &.full-width {
    padding-left: 40px;
    padding-right: 40px;
  }
}
</style>