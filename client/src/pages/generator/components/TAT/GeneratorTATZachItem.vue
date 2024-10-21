<script setup lang="ts">

import {useQuasar} from "quasar";
import {storeToRefs} from "pinia";
import useGeneratorViewStore from "stores/generatorViewStore";
import {onBeforeMount, ref, watch} from "vue";
import _ from "lodash";
import {api} from "boot/axios";

const generatorViewStore = useGeneratorViewStore();
const $q = useQuasar()
const {
  activeRpdId,
  additionalInfo,
  tatInfo,
} = storeToRefs(generatorViewStore)

const props = defineProps({
  title: {
    required: true,
  },
  type: {
    required: true,
  }
})

const main = ref('')
const about = ref('')

const passed = ref('')
const unpassed = ref('')

async function saveData() {
  $q.loading.show("Сохранение данных")
  _.set(tatInfo.value, `[0].${props.type}`, {
    "main": main.value,
    "about": about.value,
    "passed": passed.value,
    "unpassed": unpassed.value,
  })
  let r = await api.post(`/api/generator/${activeRpdId.value}/save-additional-info/`, {
    "type": 'tat',
    "value": tatInfo.value,
  })
  $q.loading.hide()
}

watch(additionalInfo, () => {
  main.value = _.get(tatInfo.value, `[0].${props.type}.main`)
  about.value = _.get(tatInfo.value, `[0].${props.type}.about`)
  passed.value = _.get(tatInfo.value, `[0].${props.type}.passed`)
  unpassed.value = _.get(tatInfo.value, `[0].${props.type}.unpassed`)
})

onBeforeMount(() => {
  main.value = _.get(tatInfo.value, `[0].${props.type}.main`)
  about.value = _.get(tatInfo.value, `[0].${props.type}.about`)
  passed.value = _.get(tatInfo.value, `[0].${props.type}.passed`)
  unpassed.value = _.get(tatInfo.value, `[0].${props.type}.unpassed`)
})

</script>

<template>
  <q-expansion-item
    :label=props.title
  >
    <q-card>
      <q-card-section>
        <div class="q-gutter-md">
          <q-input
            label="Основная информация"
            type="textarea"
            filled
            stack-label
            v-model="main"
          />
          <q-input
            label="Описание процедуры"
            type="textarea"
            filled
            stack-label
            v-model="about"
          />
          <p class="text-subtitle1">Критерии оценивания</p>
          <div class="row justify-between">
            <q-input
              label="Зачтено"
              type="textarea"
              filled
              stack-label
              v-model="passed"
              class="col q-mr-sm"
            />
            <q-input
              label="Не зачтено"
              type="textarea"
              filled
              stack-label
              v-model="unpassed"
              class="col q-ml-sm"
            />
          </div>

          <q-btn
            label="Сохранить"
            color="primary"
            @click="saveData"
          />
        </div>
      </q-card-section>
    </q-card>
  </q-expansion-item>
  <q-separator/>
</template>

<style scoped>
</style>
