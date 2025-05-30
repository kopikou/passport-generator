<script setup lang="ts">

import GeneratorTATMarkItem from "pages/generator/components/TAT/GeneratorTATMarkItem.vue";
import GeneratorTATZachItem from "pages/generator/components/TAT/GeneratorTATZachItem.vue";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {computed} from "vue";
import _ from "lodash";


const generatorViewStore = useGeneratorViewStore();

const {
  semestersData,
  admissionData,
  rpdData,
} = storeToRefs(generatorViewStore)

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

function aspGetType(dis) {
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
      <generator-t-a-t-mark-item v-if="ekzCheck" title="Экзамен" type="ekz"/>
      <generator-t-a-t-mark-item v-if="zachoCheck" title="Дифференцированный зачет" type="zacho"/>
      <generator-t-a-t-zach-item v-if="zachCheck" title="Зачет" type="zach"/>
      <generator-t-a-t-mark-item v-if="kpCheck || krCheck" title="Курсовая работа/проект" type="krkp"/>

      <generator-t-a-t-mark-item v-if="admissionData?.cadmkind == 5 && aspGetType(rpdData?.planlines?.dis) == 'foreign'"
                                 title="Кандидатский экзамен по иностранному языку" type="foreign"/>
      <generator-t-a-t-mark-item
        v-if="admissionData?.cadmkind == 5 && aspGetType(rpdData?.planlines?.dis) == 'philosophy'"
        title="Кандидатский экзамен по истории и философии науки" type="philosophy"/>
      <generator-t-a-t-mark-item
        v-if="admissionData?.cadmkind == 5 && aspGetType(rpdData?.planlines?.dis) == 'base'"
        title="Кандидатский экзамен по спец. дисциплине" type="base"/>
    </q-list>
  </div>
</template>

<style scoped>

</style>
