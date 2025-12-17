{**
 * Copyright since 2007 PrestaShop SA and Contributors
 * PrestaShop is an International Registered Trademark & Property of PrestaShop SA
 *
 * NOTICE OF LICENSE
 *
 * This source file is subject to the Academic Free License 3.0 (AFL-3.0)
 * that is bundled with this package in the file LICENSE.md.
 * It is also available through the world-wide-web at this URL:
 * https://opensource.org/licenses/AFL-3.0
 * If you did not receive a copy of the license and are unable to
 * obtain it through the world-wide-web, please send an email
 * to license@prestashop.com so we can send you a copy immediately.
 *
 * DISCLAIMER
 *
 * Do not edit or add to this file if you wish to upgrade PrestaShop to newer
 * versions in the future. If you wish to customize PrestaShop for your
 * needs please refer to https://devdocs.prestashop.com/ for more information.
 *
 * @author    PrestaShop SA and Contributors <contact@prestashop.com>
 * @copyright Since 2007 PrestaShop SA and Contributors
 * @license   https://opensource.org/licenses/AFL-3.0 Academic Free License 3.0 (AFL-3.0)
 *}
{extends file='page.tpl'}

{block name='page_title'}
  {l s='Log in to your account' d='Shop.Theme.Customeraccount'}
{/block}

{block name='page_content'}
    <div class="column-container">
        
        <div class="column column-login">
            <h2>{l s='Zaloguj się' d='Shop.Theme.Customeraccount'}</h2>
            {block name='login_form_container'}
                <section class="login-form">
                    {* To jest oryginalny formularz logowania. Usuń z niego link "Nie masz konta?" *}
                    {render file='customer/_partials/login-form.tpl' ui=$login_form}
                </section>
                {block name='display_after_login_form'}
                    {hook h='displayCustomerLoginFormAfter'}
                {/block}
                {* Oryginalny link "Nie masz konta?" jest tutaj już niepotrzebny, bo jest obok *}
            {/block}
        </div>
        
        <div class="column column-register">
            <h2>{l s='Zarejestruj się' d='Shop.Theme.Customeraccount'}</h2>
            <p>{l s='Otrzymasz liczne dodatkowe korzyści:' d='Shop.Theme.Customeraccount'}</p>
            <ul>
                <li><i class="material-icons check">check</i> {l s='podgląd statusu realizacji zamówień' d='Shop.Theme.Customeraccount'}</li>
                <li><i class="material-icons check">check</i> {l s='podgląd historii zakupów' d='Shop.Theme.Customeraccount'}</li>
                <li><i class="material-icons check">check</i> {l s='brak konieczności wprowadzania swoich danych przy kolejnych zakupach' d='Shop.Theme.Customeraccount'}</li>
                <li><i class="material-icons check">check</i> {l s='możliwość otrzymania rabatów i kuponów promocyjnych' d='Shop.Theme.Customeraccount'}</li>
            </ul>
            <a href="{$urls.pages.register}" class="btn btn-primary register-btn">{l s='ZAREJESTRUJ SIĘ' d='Shop.Theme.Customeraccount'}</a>
        </div>
        
    </div>
{/block}
