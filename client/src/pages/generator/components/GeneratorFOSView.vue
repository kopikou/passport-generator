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
  semesterYearLabel,
} = storeToRefs(generatorViewStore)

// const choicesName = ref([])
const choicesName = computed(() => {
  return _(disciplineThemes.value)
    .groupBy(x => x.semester)
    .toPairs()
    .map(pair => [pair[0], _(pair[1]).map(x => x.formcontrol_list).flatten().uniq().value()])
    .fromPairs()
    .value()
})

watch(disciplineThemes, () => {
  // const data =
  //

  // const data = _(disciplineThemes.value).groupBy(x => x.semester).value()
  // console.log(data)
  // const res = {}
  // _.forEach(data, (x, key) => {
  //     _.set(res, key,
  //       _(x).map(y => y.formcontrol_list).flatten().uniq().value()
  //     )
  //   })
  //
  // console.log(res)
  //
  //   // _(disciplineThemes.value).groupBy(x => x.semester).toPairs(x => _(x).map(y => y.formcontrol_list).flatten().uniq().value()).value()
  // const formcontrols = _(disciplineThemes.value).map(x => x.formcontrol_list).flatten().uniq().value()
  // choicesName.value = formcontrols
}, {immediate: true})

</script>

<template>
  <div class="q-px-md">
    <span class="text-h6">Оценочные материалы по дисциплине</span>
    <p></p>
    <q-separator class="q-mt-md q-mb-md"/>
    <div v-if="_.size(choicesName) > 0">
      <q-list
        bordered
        style="border-bottom: none;"
      >
        <div v-for="(items, semestr) in choicesName">
          <div v-for="(item, index) in items">
            <generator-f-o-s-item :num="semestr" :title="`${semesterYearLabel} ${semestr} | ${formControlByValue[item]?.name}`" :type="item"
                                  group="fos" :default-opened="index==0"/>
          </div>
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
