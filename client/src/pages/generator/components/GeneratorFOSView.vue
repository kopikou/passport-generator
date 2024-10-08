<script setup lang="ts">

import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {computed} from "vue";
import _ from "lodash";
import GeneratorFOSItem from "pages/generator/components/FOS/GeneratorFOSItem.vue";

const generatorViewStore = useGeneratorViewStore();

const{
  activeRpdId,
  additionalInfo,
  independentDisciplineWorkHour,
}=storeToRefs(generatorViewStore)

const choicesName = computed(() => {
  return _.uniq(_.map(independentDisciplineWorkHour.value, (x) => x.name)) || []
})

</script>

<template>
  <div style="width: 95%">
    <span class="text-h6 q-pl-lg">Фонд оценочных средст дисциплины</span>
    <p>бла бла бла</p>
    <q-separator class="q-mt-md q-mb-md"/>
    <div v-if="choicesName.length > 0">
      <q-list
      bordered
      style="border-bottom: none;"
      >
        <div v-for="n in choicesName">
          <generator-f-o-s-item :title="n" :type="n.replaceAll(' ', '')" />
        </div>
      </q-list>
    </div>
    <div v-else>
       <p class="text-h6">Не выбраны формы текущего контроля</p>
    </div>
  </div>
</template>

<style scoped>

</style>
