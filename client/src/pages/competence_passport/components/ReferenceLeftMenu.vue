<template>
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
</template>

<script setup>
import { useRoute } from 'vue-router'

const $route = useRoute()
</script>