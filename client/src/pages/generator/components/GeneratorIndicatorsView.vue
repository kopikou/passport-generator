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
      <q-list bordered>
        <div v-for="i in filteredData">
          <q-expansion-item
            :label="`${i.indicator_index} ${i.indicator}`"
          >
            <indicators-list-view :data="i"/>
          </q-expansion-item>
        </div>
      </q-list>
    </div>
  </div>
</template>

<style scoped lang="scss">


</style>
