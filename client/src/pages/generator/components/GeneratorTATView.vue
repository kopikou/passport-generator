<script setup lang="ts">

import GeneratorTATMarkItem from "pages/generator/components/TAT/GeneratorTATMarkItem.vue";
import GeneratorTATZachItem from "pages/generator/components/TAT/GeneratorTATZachItem.vue";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import _ from "lodash";


const generatorViewStore = useGeneratorViewStore();

const {
  semestersData,
  admissionData,
  rpdData,
} = storeToRefs(generatorViewStore)

function ekzCheck(item) {
  return _.get(item, 'ekz', false)
}

function zachCheck(item) {
  return _.get(item, 'zach', false)
}

function zachoCheck(item) {
  return _.get(item, 'zacho', false)
}

function kpCheck(item) {
  return _.get(item, 'kp', false)
}

function krCheck(item) {
  return _.get(item, 'kr', false)
}

function aspGetType(dis) {
  // console.log(dis)
  if (dis == 'Иностранный язык') {
    return 'foreign'
  } else if (dis == 'История и философия науки') {
    return 'philosophy'
  } else {
    return 'base'
  }
}

</script>

<template>
  <div class="q-px-md">
    <span class="text-h6">Типовые оценочные средства по дисциплине</span>
    <p></p>
    <q-separator class="q-mt-md q-mb-md"/>
    <q-list
      bordered
      style="border-bottom: none;"
    >
      <div v-for="item in semestersData">
        <generator-t-a-t-mark-item :num="item.num" v-if="ekzCheck(item)" :title="`Семестр ${item.num} | Экзамен`" type="ekz"/>
        <generator-t-a-t-mark-item :num="item.num" v-if="zachoCheck(item)" :title="`Семестр ${item.num} | Дифференцированный зачет`" type="zacho"/>
        <generator-t-a-t-zach-item :num="item.num" v-if="zachCheck(item)" :title="`Семестр ${item.num} | Зачет`" type="zach"/>
        <generator-t-a-t-mark-item :num="item.num" v-if="kpCheck(item) || krCheck(item)" :title="`Семестр ${item.num} | Курсовая работа/проект`" type="krkp"/>
        <generator-t-a-t-mark-item :num="item.num"
          v-if="admissionData?.cadmkind == 5 && aspGetType(rpdData?.planlines?.dis) == 'foreign'"
          :title="`Семестр ${item.num} | Кандидатский экзамен по иностранному языку`" type="foreign"/>
        <generator-t-a-t-mark-item :num="item.num"
          v-if="admissionData?.cadmkind == 5 && aspGetType(rpdData?.planlines?.dis) == 'philosophy'"
          :title="`Семестр ${item.num} | Кандидатский экзамен по истории и философии науки`" type="philosophy"/>
        <generator-t-a-t-mark-item :num="item.num"
          v-if="admissionData?.cadmkind == 5 && aspGetType(rpdData?.planlines?.dis) == 'base'"
          :title="`Семестр ${item.num} | Кандидатский экзамен по спец. дисциплине`" type="base"/>
      </div>
    </q-list>
  </div>
</template>

<style scoped>

</style>
