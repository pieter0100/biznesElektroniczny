<?php
/* Smarty version 3.1.48, created on 2025-10-12 17:46:18
  from '/var/www/html/themes/classic/templates/index.tpl' */

/* @var Smarty_Internal_Template $_smarty_tpl */
if ($_smarty_tpl->_decodeProperties($_smarty_tpl, array (
  'version' => '3.1.48',
  'unifunc' => 'content_68ebcd4a220ee2_16187585',
  'has_nocache_code' => false,
  'file_dependency' => 
  array (
    'c9a5cf220eb5f5748fcf152c3bf47c7237cd6b90' => 
    array (
      0 => '/var/www/html/themes/classic/templates/index.tpl',
      1 => 1702485415,
      2 => 'file',
    ),
  ),
  'includes' => 
  array (
  ),
),false)) {
function content_68ebcd4a220ee2_16187585 (Smarty_Internal_Template $_smarty_tpl) {
$_smarty_tpl->_loadInheritance();
$_smarty_tpl->inheritance->init($_smarty_tpl, true);
?>


    <?php 
$_smarty_tpl->inheritance->instanceBlock($_smarty_tpl, 'Block_50336269068ebcd4a220107_56573291', 'page_content_container');
?>

<?php $_smarty_tpl->inheritance->endChild($_smarty_tpl, 'page.tpl');
}
/* {block 'page_content_top'} */
class Block_139002956868ebcd4a220391_07526461 extends Smarty_Internal_Block
{
public function callBlock(Smarty_Internal_Template $_smarty_tpl) {
}
}
/* {/block 'page_content_top'} */
/* {block 'hook_home'} */
class Block_20680869368ebcd4a220780_39509636 extends Smarty_Internal_Block
{
public function callBlock(Smarty_Internal_Template $_smarty_tpl) {
?>

            <?php echo $_smarty_tpl->tpl_vars['HOOK_HOME']->value;?>

          <?php
}
}
/* {/block 'hook_home'} */
/* {block 'page_content'} */
class Block_166451530368ebcd4a220658_53068428 extends Smarty_Internal_Block
{
public function callBlock(Smarty_Internal_Template $_smarty_tpl) {
?>

          <?php 
$_smarty_tpl->inheritance->instanceBlock($_smarty_tpl, 'Block_20680869368ebcd4a220780_39509636', 'hook_home', $this->tplIndex);
?>

        <?php
}
}
/* {/block 'page_content'} */
/* {block 'page_content_container'} */
class Block_50336269068ebcd4a220107_56573291 extends Smarty_Internal_Block
{
public $subBlocks = array (
  'page_content_container' => 
  array (
    0 => 'Block_50336269068ebcd4a220107_56573291',
  ),
  'page_content_top' => 
  array (
    0 => 'Block_139002956868ebcd4a220391_07526461',
  ),
  'page_content' => 
  array (
    0 => 'Block_166451530368ebcd4a220658_53068428',
  ),
  'hook_home' => 
  array (
    0 => 'Block_20680869368ebcd4a220780_39509636',
  ),
);
public function callBlock(Smarty_Internal_Template $_smarty_tpl) {
?>

      <section id="content" class="page-home">
        <?php 
$_smarty_tpl->inheritance->instanceBlock($_smarty_tpl, 'Block_139002956868ebcd4a220391_07526461', 'page_content_top', $this->tplIndex);
?>


        <?php 
$_smarty_tpl->inheritance->instanceBlock($_smarty_tpl, 'Block_166451530368ebcd4a220658_53068428', 'page_content', $this->tplIndex);
?>

      </section>
    <?php
}
}
/* {/block 'page_content_container'} */
}
