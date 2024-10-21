<script setup lang="ts">

import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {computed} from "vue";
import _ from "lodash";
import GeneratorFOSItem from "pages/generator/components/FOS/GeneratorFOSItem.vue";
import EmptyIcon from "components/EmptyIcon.vue";

const generatorViewStore = useGeneratorViewStore();

const {
  activeRpdId,
  additionalInfo,
  independentDisciplineWorkHour,
  independentTypes,
} = storeToRefs(generatorViewStore)

const choicesName = computed(() => {
  return _.uniq(_.map(independentDisciplineWorkHour.value, (x) => x.name)) || []
})

function getType(value) {
  return _.filter(independentTypes.value, (x) => x.name == value)[0]?.type
}

</script>

<template>
  <div style="width: 95%">
    <span class="text-h6 q-pl-lg">Фонд оценочных средств дисциплины</span>
    <p>бла бла бла</p>
    <q-separator class="q-mt-md q-mb-md"/>
    <div v-if="choicesName.length > 0">
      <q-list
        bordered
        style="border-bottom: none;"
      >
        <div v-for="n in choicesName">
          <generator-f-o-s-item :title="n" :type="getType(n)"/>
        </div>
      </q-list>
    </div>
    <div v-else>
      <p class="text-h6">Не выбраны формы текущего контроля</p>
      <empty-icon />
    </div>
  </div>
</template>

<style scoped>

</style>
