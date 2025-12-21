<template>
  <q-list bordered class="rounded-borders reference-menu">
    <q-item-label header>Справочники</q-item-label>
    
    <q-item 
      clickable 
      v-ripple
      :to="{ name: 'competenceReference' }"
      :active="$route.name === 'competenceReference'"
      active-class="active-reference-item"
      class="reference-item"
    >
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
      active-class="active-reference-item"
      class="reference-item"
    >
      <q-item-section>
        <q-item-label>Дисциплины</q-item-label>
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
.reference-menu {
  border: 1px solid #e0e0e0;
  overflow: hidden;
  
  .q-item-label--header {
    background-color: #f5f5f5;
    font-weight: 600;
    padding: 12px 16px;
    border-bottom: 1px solid #e0e0e0;
  }
  
  .reference-item {
    min-height: 60px;
    border-bottom: 1px solid rgba(0,0,0,0.05);
    border-left: 3px solid  #8a8a8a;
    padding-left: 13px; 
    
    &:hover {
      background-color: rgba(0,0,0,0.02);
    }
    
    &:last-child {
      border-bottom: none;
    }
    
    .q-item__section--side {
      min-width: 24px;
    }
    
    .q-item__label {
      &--caption {
        opacity: 0.7;
        font-size: 12px;
      }
    }
  }
  
  .active-reference-item {
    background-color: #e3f2fd !important; 
    color: #1976d2 !important; 
    border-left: 3px solid #1976d2 !important;
    
    .q-item__label {
      &--caption {
        color: #1976d2 !important;
        opacity: 0.8;
      }
    }
    
    .q-icon {
      color: #1976d2 !important;
    }
  }
}
</style>