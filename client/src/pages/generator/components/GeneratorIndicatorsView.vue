<script setup lang="ts">
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import IndicatorsListView from "pages/generator/components/indicators/IndicatorsListView.vue";

const generatorViewStore = useGeneratorViewStore()

const {
  indicatorsData,
} = storeToRefs(generatorViewStore)

</script>

<template>
  <div>
    <div style="width: 95%">
      <span class="text-h6 q-pl-lg">Индикаторы по дисциплине</span>
      <p>бла бла бла</p>
      <q-separator class="q-mt-md q-mb-md"/>
      <div v-for="i in indicatorsData">
        <indicators-list-view  :data="i"/>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">


</style>
