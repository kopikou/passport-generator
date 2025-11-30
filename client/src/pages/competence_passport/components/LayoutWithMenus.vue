<template>
  <div class="simple-reference-layout">
    <!-- Простое верхнее меню -->
    <div class="top-menu">
      <q-tabs
        v-model="currentTab"
        class="bg-primary text-white"
        align="left"
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
    </div>

    <!-- Контент с боковым меню -->
    <div class="layout-content">
      <!-- Боковое меню -->
      <div class="sidebar">
        <q-list bordered class="rounded-borders">
          <q-item-label header>Справочники</q-item-label>
          
          <q-item 
            clickable 
            v-ripple
            :to="{ name: 'competenceReference' }"
            :active="$route.name === 'competenceReference'"
            active-class="bg-blue-1 text-primary"
          >
            <q-item-section avatar>
              <q-icon name="school" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Компетенции</q-item-label>
              <q-item-label caption>УК, ОПК, ПК</q-item-label>
            </q-item-section>
          </q-item>

          <q-item 
            clickable 
            v-ripple
            :to="{ name: 'disciplinesReference' }"
            :active="$route.name === 'disciplinesReference'"
            active-class="bg-blue-1 text-primary"
          >
            <q-item-section avatar>
              <q-icon name="menu_book" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Дисциплины</q-item-label>
              <q-item-label caption>Список всех дисциплин</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </div>

      <!-- Основной контент -->
      <main class="main-content">
        <router-view />
      </main>
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

</script>

<style scoped lang="scss">
.simple-reference-layout {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.top-menu {
  flex-shrink: 0;
}

.layout-content {
  flex: 1;
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
}
</style>