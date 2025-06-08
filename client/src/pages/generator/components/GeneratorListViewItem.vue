<script setup lang="ts">
import {GeneratorListData} from "src/types";
import {computed, ref, watch} from "vue";
import GeneratorManageDialog from "pages/generator/components/dialogs/GeneratorManageDialog.vue";
import {useQuasar} from "quasar";
import _ from "lodash";
import {storeToRefs} from "pinia";
import useGeneratorViewStore from "stores/generatorViewStore";
import {useRouter} from "vue-router";
import {api} from "boot/axios";

const props = defineProps({
  item: {
    required: true,
    type: Object as () => GeneratorListData
  },
})

const generatorViewStore = useGeneratorViewStore();
const {
  cafData,
} = storeToRefs(generatorViewStore)

const emit = defineEmits(['data-updated'])

const uploadRpdFile = ref();
const $q = useQuasar();
const router = useRouter();

const canEdit = computed(() => {
  const rules = ['person']
  return props.item.type.some(q => rules.includes(q))
})

const canView = computed(() => {
  const rules = ['rop', 'fac', 'zav']
  return props.item.type.some(q => rules.includes(q))
})

const cafDataById = computed(() => {
  return _.keyBy(cafData.value, 'value')
})

const fileName = computed(() => {
  return decodeURI(props.item?.last_accepted_file_url || "").split('/').pop()
})

function openManageDialog() {
  $q.dialog({
    component: GeneratorManageDialog,
    componentProps: {
      id: props.item.id,
      data: props.item,
    }
  }).onOk(() => {
    emit('data-updated')
  })
}

function openUrl(url: string) {
  window.open(
    url,
    '_blank' // <- This is what makes it open in a new window.
  );
}

function fileFilter(files) {
  return files.filter(file => file.type === 'application/pdf')
}

watch(() => props.item, () => {
  uploadRpdFile.value = new File([], props.item?.last_accepted_file_url || '');
}, {
  immediate: true
})

async function onFileUploaded() {
  const loadingHelpers = $q.loading.show({
    group: 'third',
    message: 'Загружаю документ',
  })
  const formData = new FormData()
  formData.append('file', uploadRpdFile.value)

  let r = await api.post(`/api/generator/${props.item.id}/upload-rpd-program/`, formData)

  emit('data-updated')

  loadingHelpers()
}

</script>

<template>
  <div>{{ item.discode }}</div>
  <div>{{ item.discpl }}</div>
  <div>{{ item.person }}</div>
  <div>{{ cafDataById[item.kafcode]?.label }}</div>
  <div>{{ item.user_confirmed_name }}</div>
  <div>{{ item.user_accepted_name }}</div>
  <div>{{ item.status_verbose }}</div>
  <div>
    <template v-if="item.can_upload_file_directly">
      <q-file :label="'Загрузить программу'" outlined bottom-slots v-model="uploadRpdFile"
              :filter="fileFilter"
              accept="*.pdf, application/pdf"
              style="width: 300px"
              @update:model-value="onFileUploaded"
              max-files="1">

        <template #file>
          {{ fileName }}
        </template>

        <template v-slot:after v-if="item.last_accepted_file_url">
          <q-btn
            icon="mdi-eye"
            flat
            dense
            style="height: 100%"
            v-show="item.last_accepted_file_url"
            color="secondary"
            @click="openUrl(item.last_accepted_file_url)"
          />
        </template>
      </q-file>
    </template>
    <template v-else>
      <q-btn v-if="canEdit" dense flat color="primary" icon="mdi-pencil"
             label="заполнить" @click="router.push(`/generator/${item.id}/main`)"/>
    </template>
    <q-btn v-if="canView" dense flat color="secondary" icon="mdi-briefcase-eye"
           label="просмотр" @click="openManageDialog"/>
  </div>
</template>

<style scoped>

</style>
