<template>
  <div class="menu-header q-pa-sm bg-grey-3">
      <div class="text-weight-bold">Справочники</div>
      <div class="text-caption text-grey ">
        Вспомогательные справочники
      </div>
  </div>    
  <q-list bordered class="reference-menu">
    <q-item 
      clickable 
      v-ripple
      :to="{ name: 'competenceReference' }"
      :active="$route.name === 'competenceReference'"
      active-class="bg-amber-2 text-black"
      class="reference-item"
    >
      <q-item-section>
        <q-item-label class="text-weight-medium">Компетенции</q-item-label>
        <q-item-label caption>Список всех компетенций</q-item-label>
      </q-item-section>
    </q-item>

    <q-item 
      clickable 
      v-ripple
      :to="{ name: 'disciplinesReference' }"
      :active="$route.name === 'disciplinesReference'"
      active-class="bg-amber-2 text-black"
      class="reference-item"
    >
      <q-item-section>
        <q-item-label class="text-weight-medium">Дисциплины</q-item-label>
        <q-item-label caption>Список всех дисциплин</q-item-label>
      </q-item-section>
    </q-item>
  </q-list>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'

const $route = useRoute()
</script>

<style scoped lang="scss">
.menu-header {
    border-bottom: 1px solid #e0e0e0;
    flex-shrink: 0;
  }

.reference-menu {
  .q-item-label--header {
    border-bottom: 1px solid rgba(0,0,0,0.05);
  }
  
  .reference-item {
    min-height: 60px;
  }

}
</style>