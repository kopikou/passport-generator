<script setup lang="ts">
import EmptyIcon from "components/EmptyIcon.vue";
import LayoutHCF from "components/LayoutHCF.vue";
import {ref} from "vue";

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

const emit = defineEmits(["addClicked"])

const tab = defineModel('tab', {
  default: 0
});

</script>

<template>
  <layout-h-c-f>
    <template #header>
      <div class="q-pa-sm">
        <div style="display:flex; justify-content: space-between; margin-bottom: 0.5rem">
          <slot name="header">
            <div class="q-mb-sm" style="font-size: 1.25rem">{{ title }}</div>
            <q-btn v-if="allPercent > 0" :label="buttonAddTitle" color="white" text-color="black" icon="mdi-plus" @click="emit('addClicked')"
                   :disabled="disabled"/>
          </slot>
        </div>
        <div v-if="allPercent != 0">
          <q-linear-progress class="q-mb-md" size="20px" rounded :value="allPercentValue / allPercent" color="teal-3">
            <div class="absolute-full flex flex-center">
              <q-badge color="white" text-color="black" :label="`${allPercentValue} / ${allPercent}`"/>
            </div>
          </q-linear-progress>
          <q-tabs
            v-model="tab"
            align="left"
            narrow-indicator
            class="q-mb-md"
          >
            <q-tab v-for="item in semestersData" :name="`${item.num}`"
                   :label="`Семестр ${item.num}`"/>
          </q-tabs>
          <q-linear-progress class="q-mb-md" size="20px" rounded :value="allSemesterPercentValue / allSemesterPercent"
                             color="purple-3">
            <div class="absolute-full flex flex-center">
              <q-badge color="white" text-color="black" :label="`${allSemesterPercentValue} / ${allSemesterPercent}`"/>
            </div>
          </q-linear-progress>
        </div>
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
  </layout-h-c-f>
</template>

<style scoped lang="scss">

</style>
