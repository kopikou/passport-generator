<script setup lang="ts">
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import IndicatorsListView from "pages/generator/components/indicators/IndicatorsListView.vue";
import {computed} from "vue";
import _ from "lodash";

const generatorViewStore = useGeneratorViewStore()

const {
  indicatorsData,
  admissionData,
} = storeToRefs(generatorViewStore)


const filteredData = computed(() => {
  return _.orderBy(indicatorsData.value, x => x.indicator_index)
})

</script>

<template>
  <div class="q-px-md">
      <span v-if="admissionData.cadmkind != 5" class="text-h6">Индикаторы по дисциплине</span>
      <span v-else class="text-h6">Результаты освоения дисциплины</span>
      <p>Раскройте для заполнения</p>
      <q-separator class="q-mt-md q-mb-md"/>
      <q-list bordered>
        <div v-for="(i, index) in filteredData">
          <q-expansion-item
            :label="`${i.indicator_index} ${i.indicator}`"
            :default-opened="index==0"
            group="indicators"
          >
            <indicators-list-view :data="i"/>
          </q-expansion-item>
        </div>
      </q-list>
  </div>
</template>

<style scoped lang="scss">


</style>
