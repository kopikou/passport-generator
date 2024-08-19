<script setup lang="ts">

const props = defineProps({
  id: {
    required: true,
  }
})

const menuItems = [
  {title: 'Титульный лист', url: 'main'},
  {title: 'Компетенции', url: 'competences'},
  {title: 'Индикаторы', url: 'indicators'},
  {title: 'Место дисциплины в структуре ООП', url: 'discipline-place'},
  {title: 'Структура дисциплины', url: 'structure'},
  {title: 'Содержание тем дисциплины', url: 'discipline-theme'},
  {title: 'Содержание лабораторных работ', url: 'discipline-lab'},
  {title: 'Содержание практических работ', url: 'discipline-practice'},
  {title: 'Содержание самостоятельных работ', url: 'discipline-independent'},
  {title: 'Литература', url: 'library'},
  {title: 'Использованные результаты НИОКР', url: 'rdw'},
  {title: 'Использованное программное обеспечение', url: 'soft'},
  {title: 'Используемое материально-техническое обеспечение', url: 'logistics'},
]

</script>

<template>
  <q-list
    bordered
    separator
    style="width: 95%;"
  >
    <q-item
      v-for="item in menuItems"
      clickable
      v-ripple
      active-class="bg-amber-4 text-black"
      :to="`/generator/${id}/${item.url}`"
    >
      <q-item-section>
        <q-item-label>{{ item.title }}</q-item-label>
<!--        <q-item-label caption>Основная информация о программе</q-item-label>-->
      </q-item-section>
    </q-item>

  </q-list>
</template>

<style scoped>

</style>
