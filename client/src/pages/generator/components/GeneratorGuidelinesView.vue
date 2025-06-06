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
  <div class="q-px-md">
    <span class="text-h6">Методические указания по дисциплине</span>
    <p>Вы можете написать ссылку на электронный курс из <a href="https://el.istu.edu">el.istu.edu</a> оформленный по <a
      href="https://bibliostyle.ru/oformlenie-ssylok-na-elektronnye-dokumenty-sayty-internet-istochniki-po-gost-p-7-0-108-2022/"
      target="_blank">ГОСТ 7.0.108-2022</a></p>
    <q-separator class="q-mt-md q-mb-md"/>
    <q-list
      bordered
      style="border-bottom: none;"
    >
      <GuidelinesExpansionItem v-if="labCheck" label="Лабораторные работы" type="laboratory" :default-opened="true"
                               group="info"/>
      <GuidelinesExpansionItem v-if="prCheck" label="Практические занятия" type="practice" :default-opened="true"
                               group="info"/>
      <GuidelinesExpansionItem v-if="srsCheck" label="Самостоятельные занятия" type="independent" :default-opened="true"
                               group="info"/>
      <GuidelinesExpansionItem v-if="krCheck || kpCheck" label="Курсовой проект/работа" type="course"
                               :default-opened="true" group="info"/>
    </q-list>
  </div>
</template>

<style scoped>

</style>
