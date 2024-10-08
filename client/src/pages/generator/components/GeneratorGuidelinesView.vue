<script setup lang="ts">

import GuidelinesExpansionItem from "pages/generator/components/guidelines/GuidelinesExpansionItem.vue";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {computed} from "vue";
import _ from "lodash";


const generatorViewStore = useGeneratorViewStore();

const {
  semestersData,
} = storeToRefs(generatorViewStore)


const labCheck = computed(() => {
  return _.sum(_.map(semestersData.value, (x) => x.lab))
})

const prCheck = computed(() => {
  return _.sum(_.map(semestersData.value, (x) => x.pr))
})

const srsCheck = computed(() => {
  return _.sum(_.map(semestersData.value, (x) => x.srs))
})

const krCheck = computed(() => {
  return _.sum(_.map(semestersData.value, (x) => x.kr_hour))
})

const kpCheck = computed(() => {
  return _.sum(_.map(semestersData.value, (x) => x.kp_hour))
})

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
      <div v-show="labCheck">
        <GuidelinesExpansionItem label="Лабораторные работы" type="laboratory"/>
      </div>
      <div v-show="prCheck">
        <GuidelinesExpansionItem label="Практические занятия" type="practice"/>
      </div>
      <div v-show="srsCheck">
        <GuidelinesExpansionItem label="Самостоятельные занятия" type="independent"/>
      </div>
      <div v-show="krCheck || kpCheck">
        <GuidelinesExpansionItem label="Курсовой проект/работа" type="course"/>
      </div>
    </q-list>
  </div>
</template>

<style scoped>

</style>
