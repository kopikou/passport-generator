<script setup lang="ts">

import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {ref, watch} from "vue";
import _ from "lodash";
import GeneratorFOSItem from "pages/generator/components/FOS/GeneratorFOSItem.vue";
import EmptyIcon from "components/EmptyIcon.vue";

const generatorViewStore = useGeneratorViewStore();

const {
  activeRpdId,
  disciplineThemes,
} = storeToRefs(generatorViewStore)

const choicesName = ref([])

watch(disciplineThemes, () => {
  choicesName.value = _.uniqBy(disciplineThemes.value, 'formcontrol_verbose')
}, {immediate: true})

</script>

<template>
  <div class="q-px-md">
    <span class="text-h6">Оценочные материалы по дисциплине</span>
    <p></p>
    <q-separator class="q-mt-md q-mb-md"/>
    <div v-if="choicesName.length > 0">
      <q-list
        bordered
        style="border-bottom: none;"
      >
        <div v-for="(n, index) in choicesName">
          <generator-f-o-s-item :title="n.formcontrol_verbose" :type="n.formcontrol_id" group="fos" :default-opened="index==0"/>
        </div>
      </q-list>
    </div>
    <div v-else>
      <p class="text-h6">Не выбраны формы текущего контроля</p>
      <empty-icon/>
    </div>
  </div>
</template>

<style scoped>

</style>
