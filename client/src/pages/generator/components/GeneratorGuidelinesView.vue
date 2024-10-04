<script setup lang="ts">

import GuidelinesExpansionItem from "pages/generator/components/guidelines/GuidelinesExpansionItem.vue";
</script>

<template>
  <div style="width: 95%">
    <span class="text-h6 q-pl-lg">Методические указания по дисциплине</span>
    <p>бла бла бла</p>
    <q-separator class="q-mt-md q-mb-md"/>
    <q-list
        bordered
        style="border-bottom: none;"
    >
      <div>
          <GuidelinesExpansionItem label="Лабораторные работы" type="laboratory"/>
      </div>
      <div>
          <GuidelinesExpansionItem label="Практические занятия" type="practice"/>
      </div>
      <div>
          <GuidelinesExpansionItem label="Самостоятельные занятия" type="independent"/>
      </div>
      <div>
          <GuidelinesExpansionItem label="Курсовой проект/работа" type="course"/>
      </div>
    </q-list>
  </div>
</template>

<style scoped>

</style>
