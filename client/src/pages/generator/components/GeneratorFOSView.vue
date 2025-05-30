<script setup lang="ts">

import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {computed, ref, watch} from "vue";
import _ from "lodash";
import GeneratorFOSItem from "pages/generator/components/FOS/GeneratorFOSItem.vue";
import EmptyIcon from "components/EmptyIcon.vue";

const generatorViewStore = useGeneratorViewStore();

const {
  activeRpdId,
  disciplineThemes,
  formControlByValue,
} = storeToRefs(generatorViewStore)

const choicesName = ref([])


watch(disciplineThemes, () => {
  const formcontrols = _(disciplineThemes.value).map(x => x.formcontrol_list).flatten().uniq().value()
  choicesName.value = formcontrols
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
          <generator-f-o-s-item :title="formControlByValue[n].name" :type="n" group="fos" :default-opened="index==0"/>
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
