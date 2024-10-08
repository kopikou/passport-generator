<script setup lang="ts">

import GeneratorTATMarkItem from "pages/generator/components/TAT/GeneratorTATMarkItem.vue";
import GeneratorTATZachItem from "pages/generator/components/TAT/GeneratorTATZachItem.vue";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {computed} from "vue";
import _ from "lodash";


const generatorViewStore = useGeneratorViewStore();

const{
  semestersData,
}=storeToRefs(generatorViewStore)

const ekzCheck = computed(() => {
  return _.some(semestersData.value, {'ekz': true})
})

const zachCheck = computed(() => {
  return _.some(semestersData.value, {'zach': true})
})

const zachoCheck = computed(() => {
  return _.some(semestersData.value, {'zacho': 1})
})

const kpCheck = computed(() => {
  return _.some(semestersData.value, {'kp': true})
})

const krCheck = computed(() => {
  return _.some(semestersData.value, {'kr': true})
})


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
      <generator-t-a-t-mark-item v-if="ekzCheck" title="Экзамен" type="ekz"/>
      <generator-t-a-t-mark-item v-if="zachoCheck" title="Дифференцированный зачет" type="zacho"/>
      <generator-t-a-t-zach-item v-if="zachCheck" title="Зачет" type="zach"/>
      <generator-t-a-t-mark-item v-if="kpCheck || krCheck" title="Курсовая работа/проект" type="krkp"/>
    </q-list>
  </div>
</template>

<style scoped>

</style>
