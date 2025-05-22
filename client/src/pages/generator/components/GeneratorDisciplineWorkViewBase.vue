<script setup lang="ts">
import EmptyIcon from "components/EmptyIcon.vue";
import LayoutHCF from "components/LayoutHCF.vue";
import {computed, ref} from "vue";
import GeneratorPageView from "pages/generator/components/GeneratorPageView.vue";
import useGeneratorViewStore from "stores/generatorViewStore";

const props = defineProps({
  disabled: Boolean,
  allPercent: Number,
  allPercentValue: Number,
  semestersData: Array<Object>,
  allSemesterPercentValue: Number,
  allSemesterPercent: Number,
  title: String,
  buttonAddTitle: String
})

const generatorViewStore = useGeneratorViewStore();

const emit = defineEmits(["addClicked"])

const tab = defineModel('tab', {
  default: 0
});



</script>

<template>
  <generator-page-view :title="title">
    <template #title-right>
      <q-btn v-if="allPercent > 0" :label="buttonAddTitle" color="white" text-color="black" icon="mdi-plus"
             @click="emit('addClicked')"
             :disabled="disabled"/>
    </template>
    <template #header>
      <div v-if="allPercent != 0">
        <q-linear-progress class="q-mb-md" size="20px" rounded :value="allPercentValue / allPercent" color="teal-3">
          <div class="absolute-full flex flex-center">
            <q-badge color="white" text-color="black" :label="`${allPercentValue} / ${allPercent}`"/>
          </div>
        </q-linear-progress>
        <q-tabs
          v-model="tab"
          align="left"
          active-bg-color="teal-1"
          class="q-mb-md"
        >
          <q-tab class="text-teal" v-for="item in semestersData" :name="item.num"
                 :label="`${generatorViewStore.semesterYearLabel} ${item.num}`"/>
          <q-tab class="text-teal" :name="-1">Все</q-tab>
        </q-tabs>
        <q-linear-progress class="q-mb-md" size="20px" rounded :value="allSemesterPercentValue / allSemesterPercent"
                           color="orange-3">
          <div class="absolute-full flex flex-center">
            <q-badge color="white" text-color="black"
                     :label="`${allSemesterPercentValue} / ${allSemesterPercent}`"/>
          </div>
        </q-linear-progress>
      </div>
    </template>
    <template #content>
      <div v-if="allPercent != 0">
        <slot name="content"></slot>
      </div>
      <div v-else class="q-pa-md">
        <p class="text-h6">Нет часов</p>
        <empty-icon/>
      </div>
    </template>
  </generator-page-view>
</template>

<style scoped lang="scss">

</style>
