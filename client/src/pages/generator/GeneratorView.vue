<script setup lang="ts">

import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {computed, watch} from "vue";
import _ from "lodash";
import {useQuasar} from "quasar";
import {useRouter} from "vue-router";
import GeneratorLeftMenu from "pages/generator/components/GeneratorLeftMenu.vue";
import GeneratorCopyDialog from "pages/generator/components/dialogs/GeneratorCopyDialog.vue";
import useMainStore from "stores/mainStore";
import {api} from "boot/axios";

const generatorViewStore = useGeneratorViewStore();


const mainStore = useMainStore();
const {
  FORCE_SCRIPT_NAME
} = storeToRefs(mainStore)


const $q = useQuasar()
const router = useRouter()

const {
  cafData,
  activeRpdId,
  rpdData,
  criticalErrors,
  disabled,
  statusVerbose,
  planlinesData,
} = storeToRefs(generatorViewStore)

const props = defineProps({
    id: {
      required: true
    }
  }
)

const cafDataById = computed(() => {
  return _.keyBy(cafData.value, 'value')
})

function copyProgram() {
  $q.dialog({
    component: GeneratorCopyDialog,
  }).onOk((data) => {
    // console.log(data)
  })
}


async function sendToReview() {
  $q.loading.show()
  let r = await api.get(`/api/generator/${activeRpdId.value}/send-rpd-on-review/`)
  rpdData.value.status = r.data.status
  rpdData.value.status_verbose = r.data.status_verbose
  $q.loading.hide()
}

async function sendToApprove() {
  $q.loading.show()
  let r = await api.post(`/api/generator/${activeRpdId.value}/accept-rpd/`)
  rpdData.value.status = r.data.status
  rpdData.value.status_verbose = r.data.status_verbose
  await generatorViewStore.getData()
  $q.loading.hide()
}


async function onEditClick() {
  $q.dialog({
    message: "Подтвердите, что хотите скорректировать план. После корректировки РПД, вам необходимо будет снова переутвердить РПД",
    cancel: true,
  }).onOk(async () => {
      $q.loading.show()
      let r = await api.get(`/api/generator/${activeRpdId.value}/send-rpd-on-edit/`)
      rpdData.value.status = r.data.status
      rpdData.value.status_verbose = r.data.status_verbose
      $q.loading.hide()
  })
}


watch(() => props.id,
  () => {
    activeRpdId.value = props.id
  },
  {immediate: true})

</script>

<template>
  <div class="generator-container">
    <div class="generator-container__header">
      <div style="display: flex; align-items: center; gap: 8px">
        <q-btn
          dense
          color="purple-4"
          icon="mdi-chevron-left"
          @click="router.push('/generator/')"
        />
        <span class="abbrprofile" style="font-size: 1.5rem">{{ rpdData.planlines?.plan.abbrprofile }} {{
            rpdData.planlines?.plan.startyear
          }} {{ rpdData.planlines?.dis }}
      </span>
      </div>
      <div style="justify-content: flex-end; display: flex; gap: 8px">
        <q-btn
          color="purple-5"
          label="Выгрузить в PDF"
          no-caps
          icon="mdi-file-pdf-box"
          :href="`${FORCE_SCRIPT_NAME}/api/generator/${props.id}/get-rpd-report/`"
          target="_blank"
        />
        <q-btn
          label="Скопировать"
          color="white"
          text-color="black"
          icon="mdi-content-copy"
          @click="copyProgram"
        />
        <q-btn v-if="!disabled"
               color="secondary"
               @click="planlinesData.viewpract ? sendToApprove() : sendToReview()"
               :label="planlinesData.viewpract ? 'Утвердить' : 'Отправить на согласование'"
               :disabled="criticalErrors.length != 0"
        />
        <template v-else>
          <q-btn-group push>
            <q-btn
              color="secondary"
              disable
              :label="statusVerbose"
            />
            <q-btn color="teal-2" text-color="black" v-if="statusVerbose == 'Утвержден'" icon="mdi-pencil" @click="onEditClick">
            </q-btn>
          </q-btn-group>
        </template>

      </div>
    </div>
    <div class="generator-container__menu">
      <!--      <div class="text-subtitle1 q-pl-md">{{ rpdData.planlines?.plan.abbrprofile }} {{-->
      <!--          rpdData.planlines?.plan.startyear-->
      <!--        }} {{ rpdData.planlines?.dis }}-->
      <!--      </div>-->
      <generator-left-menu :id="props.id"/>
    </div>
    <div class="generator-container__content">
      <router-view/>
    </div>
  </div>
</template>

<style scoped lang="scss">

.generator-container {
  display: grid;
  grid-template-columns: 20% auto;
  grid-template-rows: auto 1fr;
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  grid-template-areas:
  "h h"
  "m c";
}

.generator-container__buttons {
  grid-area: a;
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 8px;
  padding: 8px;
  border-bottom: 2px solid silver;
}

.generator-container__header {
  background: $grey-4;
  grid-area: h;
  display: grid;
  grid-template-columns: auto 1fr;
  padding: 0.5rem;
  //font-size: 1.25rem;
  border-bottom: 2px solid silver;
  box-shadow: 0 0 8px silver;

  .abbrprofile {
    background: linear-gradient(90deg, $purple-2, $orange-2);
  }
}

.generator-container__menu {
  overflow-y: auto;
  grid-area: m;
  background: $grey-2;
  border-right: 2px solid silver;
  box-shadow: 0 0 8px silver;
}

.generator-container__content {
  overflow-y: auto;
  grid-area: c;
  padding-top: 8px;
  position: relative;
}

</style>
