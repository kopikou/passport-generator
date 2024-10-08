<script setup lang="ts">

import GeneratorTATItem from "pages/generator/components/TAT/GeneratorTATItem.vue";
import GeneratorTATMarkItem from "pages/generator/components/TAT/GeneratorTATMarkItem.vue";
import GeneratorTATZachItem from "pages/generator/components/TAT/GeneratorTATZachItem.vue";
</script>

<template>
  <div style="width: 95%">
    <span class="text-h6 q-pl-lg">Типовые оценочные средства по дисциплине</span>
    <p>бла бла бла</p>
    <q-separator class="q-mt-md q-mb-md"/>
    <q-list
      bordered
      style="border-bottom: none;"
    >
      <generator-t-a-t-mark-item title="Экзамен" type="ekz"/>
      <generator-t-a-t-mark-item title="Дифференцированный зачет" type="zacho"/>
      <generator-t-a-t-zach-item title="Зачет" type="zach"/>
      <generator-t-a-t-mark-item title="Курсовая работа/проект" type="krkp"/>
    </q-list>
  </div>
</template>

<style scoped>

</style>
