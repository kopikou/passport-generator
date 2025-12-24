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

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import TopNavigationMenu from './TopNavigationMenu.vue'
import ReferenceLeftMenu from './ReferenceLeftMenu.vue'
import PassportLeftMenu from './PassportLeftMenu.vue'

const $route = useRoute()

// Определяем, какое меню показывать в зависимости от маршрута
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
  width: 20%;
  border-right: 2px solid silver;
  box-shadow: 0 0 8px silver;
  overflow-y: auto;
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