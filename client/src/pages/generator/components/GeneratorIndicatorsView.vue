<script setup lang="ts">
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import IndicatorsListView from "pages/generator/components/indicators/IndicatorsListView.vue";
import {computed} from "vue";
import _ from "lodash";

const generatorViewStore = useGeneratorViewStore()

const {
  indicatorsData,
} = storeToRefs(generatorViewStore)


const filteredData = computed(() => {
  return _.orderBy(indicatorsData.value, x => x.indicator_index)
})

</script>

<template>
  <div>
    <div style="width: 95%">
      <span class="text-h6 q-pl-lg">Индикаторы по дисциплине</span>
      <p></p>
      <q-separator class="q-mt-md q-mb-md"/>
      <div v-for="i in filteredData">
        <indicators-list-view  :data="i"/>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">


</style>
