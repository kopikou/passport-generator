<template>
  <TopNavigationMenu>
    <template #content>
      <div class="layout-content">
        <!-- Боковое меню -->
        <div class="sidebar" v-if="showSidebar">
          <component :is="currentSidebar" />
        </div>

        <!-- Основной контент -->
        <main class="main-content" :class="{ 'full-width': !showSidebar }">
          <router-view />
        </main>
      </div>
    </template>
  </TopNavigationMenu>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import TopNavigationMenu from './TopNavigationMenu.vue'
import ReferenceLeftMenu from './ReferenceLeftMenu.vue'
import PassportLeftMenu from './PassportLeftMenu.vue'

const $route = useRoute()

// Определяем, какой сайдбар показывать в зависимости от маршрута
const currentSidebar = computed(() => {
  const routeName = $route.name
  
  if (routeName?.startsWith('competenceReference') || 
      routeName?.startsWith('disciplinesReference')) {
    return ReferenceLeftMenu
  }
  
  if (routeName?.startsWith('competencePassport')) {
    return PassportLeftMenu
  }
  
  return null
})

const showSidebar = computed(() => {
  return currentSidebar.value !== null
})
</script>

<style scoped lang="scss">
.layout-content {
  height: 100%;
  display: flex;
  overflow: hidden;
}

.sidebar {
  width: 280px;
  background: #f8f9fa;
  border-right: 1px solid #e0e0e0;
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