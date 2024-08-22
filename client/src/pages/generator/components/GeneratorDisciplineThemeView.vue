<script setup lang="ts">
import {ref} from "vue";
import {useQuasar} from "quasar";
import GeneratorDialogAddTheme from "pages/generator/components/dialogs/GeneratorDialogAddTheme.vue";

const $q = useQuasar()




const tab = ref(0)

function addTheme() {
  $q.dialog({
    component: GeneratorDialogAddTheme,
    componentProps: {
      id: tab.value
    },
  })
}

</script>

<template>
  <div>
    <div style="width: 95%">
      <span class="text-h6 q-pl-lg">Содержание разделов и тем по дисциплине</span>
      <p>бла бла бла</p>
      <q-separator class="q-mt-md q-mb-md"/>
      <q-btn label="Добавить тему дисциплины" color="teal" class="q-mb-md" @click="addTheme"/>
      <q-tabs
          v-model="tab"
          align="left"
          narrow-indicator
          class="q-mb-md"
      >
        <q-tab class="text-teal bg-grey-4" name="1" label="1"/>
        <q-tab class="text-teal bg-grey-4" name="2" label="2"/>
      </q-tabs>
      <q-tab-panels
          v-model="tab"
          animated
          transition-prev="scale"
          transition-next="scale"
      >
        <q-tab-panel v-for="i in 2" :name="`${i}`">
          hello world
        </q-tab-panel>
      </q-tab-panels>
    </div>
  </div>
</template>

<style scoped>

</style>
