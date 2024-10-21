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
  },
})

const main = ref('')
const about = ref('')

const great = ref('')
const good = ref('')
const satisfactorily = ref('')
const unsatisfactory = ref('')

async function saveData() {
  $q.loading.show("Сохранение данных")
  _.set(tatInfo.value, `[0].${props.type}`, {
    "main": main.value,
    "about": about.value,
    "great": great.value,
    "good": good.value,
    "satisfactorily": satisfactorily.value,
    "unsatisfactory": unsatisfactory.value,
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
  great.value = _.get(tatInfo.value, `[0].${props.type}.great`)
  good.value = _.get(tatInfo.value, `[0].${props.type}.good`)
  satisfactorily.value = _.get(tatInfo.value, `[0].${props.type}.satisfactorily`)
  unsatisfactory.value = _.get(tatInfo.value, `[0].${props.type}.unsatisfactory`)
})

onBeforeMount(() => {
  main.value = _.get(tatInfo.value, `[0].${props.type}.main`)
  about.value = _.get(tatInfo.value, `[0].${props.type}.about`)
  great.value = _.get(tatInfo.value, `[0].${props.type}.great`)
  good.value = _.get(tatInfo.value, `[0].${props.type}.good`)
  satisfactorily.value = _.get(tatInfo.value, `[0].${props.type}.satisfactorily`)
  unsatisfactory.value = _.get(tatInfo.value, `[0].${props.type}.unsatisfactory`)
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
              label="Отлично"
              type="textarea"
              filled
              stack-label
              v-model="great"
              class="col q-mr-sm"
            />
            <q-input
              label="Хорошо"
              type="textarea"
              filled
              stack-label
              v-model="good"
              class="col q-ml-sm"
            />
          </div>
          <div class="row justify-between">
            <q-input
              label="Удовлетворительно"
              type="textarea"
              filled
              stack-label
              v-model="satisfactorily"
              class="col q-mr-sm"
            />
            <q-input
              label="Неудовлетворительно"
              type="textarea"
              filled
              stack-label
              v-model="unsatisfactory"
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
